"""
Test script to verify MediaPipe pose detection is working correctly.
This will help debug the rep counting issue by showing detected angles in real-time.
"""
import cv2
from app.utils.pose_utils import detect_pose, bicep_curl

def main():
    print("🎥 Starting camera test...")
    print("Instructions:")
    print("  - Stand in front of the camera")
    print("  - Make sure your full body is visible")
    print("  - Perform bicep curls slowly")
    print("  - Press 'q' to quit\n")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    count = 0
    stage = 'ready'
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        # Detect pose
        landmarks = detect_pose(frame)
        
        if landmarks:
            # Calculate angles
            left_angle, right_angle = bicep_curl(landmarks)
            
            if left_angle and right_angle:
                # Use the smaller angle (the arm being used)
                angle = min(left_angle, right_angle)
                
                # Rep counting logic (same as in process_frame)
                if angle > 160:
                    if stage != 'down':
                        stage = 'down'
                        
                elif angle < 40:
                    if stage == 'down':
                        stage = 'up'
                        count += 1
                        print(f"✅ Rep #{count} completed!")
                
                elif 40 <= angle <= 160:
                    if stage == 'up' and angle > 90:
                        stage = 'down'
                
                # Display info on frame
                cv2.putText(frame, f'Left Angle: {int(left_angle)}', 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f'Right Angle: {int(right_angle)}', 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f'Stage: {stage}', 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(frame, f'Count: {count}', 
                           (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                
                # Color indicator based on stage
                if stage == 'down':
                    cv2.rectangle(frame, (0, 0), (frame.shape[1], 10), (0, 0, 255), -1)
                elif stage == 'up':
                    cv2.rectangle(frame, (0, 0), (frame.shape[1], 10), (0, 255, 0), -1)
            else:
                cv2.putText(frame, 'Angles not detected', 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, 'No pose detected - move into frame', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow('Pose Detection Test - Press Q to quit', frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n🏁 Test completed. Total reps: {count}")

if __name__ == "__main__":
    main()
